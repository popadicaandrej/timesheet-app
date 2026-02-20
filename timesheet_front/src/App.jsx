import { useState } from 'react'
import './App.css'

function App() {
  const [name, setName] = useState('')
  const [date, setDate] = useState(() => {
    const today = new Date()
    return today.toISOString().split('T')[0]
  })
  const [hours, setHours] = useState('')
  const [project, setProject] = useState('')
  const [description, setDescription] = useState('')
  const [successMessage, setSuccessMessage] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    setSuccessMessage('')

    // Validacija
    if (!name) {
      alert('Molimo izaberite ime.')
      return
    }

    if (!hours || isNaN(parseFloat(hours)) || parseFloat(hours) <= 0) {
      alert('Molimo unesite validan broj sati (veći od 0).')
      return
    }

    if (!description.trim()) {
      alert('Molimo unesite opis.')
      return
    }

    // Ako je validacija prošla
    setSuccessMessage('✅ Sačuvano!')
    
    // Očisti Hours, Project, Description, ali ostavi Name i Date
    setHours('')
    setProject('')
    setDescription('')
  }

  return (
    <div className="app-container">
      <h1>Timesheet App</h1>
      <form onSubmit={handleSubmit} className="timesheet-form">
        <div className="form-group">
          <label>Name: <span className="required">*</span></label>
          <div className="radio-group">
            {['Danilo Bajić', 'Relja Diklić', 'Vuk Stanković', 'Vuk Knežević', 'Lazar Djordjević', 'Dušan Stojanović', 'Mila Dobrić'].map((option) => (
              <label key={option} className="radio-label">
                <input
                  type="radio"
                  name="employee"
                  value={option}
                  checked={name === option}
                  onChange={(e) => setName(e.target.value)}
                />
                {option}
              </label>
            ))}
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="date">Date: <span className="required">*</span></label>
          <input
            type="date"
            id="date"
            value={date}
            disabled
            className="date-input"
          />
        </div>

        <div className="form-group">
          <label htmlFor="hours">Hours: <span className="required">*</span></label>
          <input
            type="number"
            id="hours"
            value={hours}
            onChange={(e) => setHours(e.target.value)}
            step="0.25"
            min="0"
            placeholder="0.00"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="project">Project:</label>
          <input
            type="text"
            id="project"
            value={project}
            onChange={(e) => setProject(e.target.value)}
            placeholder="Naziv projekta"
          />
        </div>

        <div className="form-group">
          <label htmlFor="description">Description: <span className="required">*</span></label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows="4"
            placeholder="Opis rada"
            required
          />
        </div>

        <button type="submit" className="submit-button">Submit</button>

        {successMessage && (
          <div className="success-message">{successMessage}</div>
        )}
      </form>
    </div>
  )
}

export default App
