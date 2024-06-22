import { useState } from 'react'
import TextBox from './components/TextBox'
import './App.css'

const App = () => {
  return (
    <div className="App">
      <header className="App-header">
          <h1>Consensus AI</h1>
      </header>
      <main>
          <TextBox />
      </main>
    </div>
  )
}

export default App
