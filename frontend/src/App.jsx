import { useState } from 'react'
import './App.css'

function App() {
  const [url, setUrl] = useState('')
  const [shortUrl, setShortUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [copied, setCopied] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    setShortUrl('')
    setCopied(false)

    try {
      const response = await fetch(`/shorten`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ redirect_to: url }),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Ошибка при создании ссылки')
      }

      const data = await response.json()
      const fullShortUrl = `${window.location.origin}/${data.code}`
      setShortUrl(fullShortUrl)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(shortUrl)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (err) {
      console.error('Failed to copy:', err)
    }
  }

  return (
    <div className="container">
      <header>
        <h1>🔗 URL Shortener</h1>
        <p>Сократите вашу ссылку за секунду</p>
      </header>

      <main>
        <form onSubmit={handleSubmit} className="shorten-form">
          <div className="form-group">
            <label htmlFor="url">Введите длинную ссылку:</label>
            <input
              type="url"
              id="url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="https://example.com/very-long-url"
              required
            />
          </div>

          <button type="submit" disabled={loading} className="btn-submit">
            {loading ? '⏳ Создаю...' : 'Сократить'}
          </button>
        </form>

        {error && (
          <div className="error">
            <p>⚠️ {error}</p>
          </div>
        )}

        {shortUrl && (
          <div className="result">
            <p className="result-label">Ваша короткая ссылка:</p>
            <div className="short-url-container">
              <input
                type="text"
                value={shortUrl}
                readOnly
                className="short-url-input"
              />
              <button onClick={handleCopy} className="btn-copy">
                {copied ? '✓ Скопировано' : 'Копировать'}
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

export default App