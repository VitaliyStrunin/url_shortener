from sqlalchemy import update
import logging
import asyncio

from src.core.celery_config import celery_app
from src.database.redis.redis import get_redis_client
from src.database.engine import engine
from src.urls.infrastructure.database.orm import ShortURLDB



logger = logging.getLogger(__name__)


@celery_app.task(name="sync_analytics_to_db")
def sync_analytics_to_db():
    asyncio.run(_sync_analytics_to_db())

async def _sync_analytics_to_db():
    logger.info("Started logging analytics to databse")
    
    redis_client = get_redis_client()
    analytics_prefix = "analytics:redirects:"
    
    try:
        keys = []
        async for key in redis_client.scan_iter(f"{analytics_prefix}*"):
            keys.append(key)
        if not keys:
            logger.info("No data to sync")
            return
        
        logger.info(f"Found {len(keys)} links to sync")
        
        updates = []
        for key in keys:
            count = await redis_client.get(key)
            if count:
                code = key.replace(analytics_prefix, "")
                updates.append((code, int(count)))
                
        async with engine.begin() as session:
            for code, count in updates:
                await session.execute(
                    update(ShortURLDB)
                    .where(ShortURLDB.code == code)
                    .values(redirect_amount = ShortURLDB.redirect_amount + count)
                )
                logger.debug(f"Updated {code} with {count} redirects")
            await session.commit()
        
        for key in keys:
            await redis_client.delete(key)
        
        logger.info(f"Succesfully synced {len(updates)} links")
        
    except Exception as e:
        logger.error(f"Error during analytics sync: ", str(e))
        raise
    finally:
        await redis_client.close()