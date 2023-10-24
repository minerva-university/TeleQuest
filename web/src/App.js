import React from 'react';
import './App.css';
import robot from './robot.svg';

import JSConfetti from 'js-confetti'

const jsConfetti = new JSConfetti()

const App = () => {
  const triggerConfetti = () => {
    jsConfetti.addConfetti();
  };
  return (
    <div className="container">
      <header>
        <h1>Telequest</h1>
        <p>A unique answer to your questions.</p>
        <p>Available exclusively at Telegram.</p>
      </header>

      <nav>
        <button>Home</button>
        <button>About</button>
        <button>Contact</button>
      </nav>

      <section className="main-content">
        <h2>Great for big Telegram chats</h2>
        <p>Powered by OpenAI API.</p>
        <button>Get Started</button>

        <div className="illustration">
          <img src={robot} alt="Chatbot Illustration" />
        </div>

        <h3>Currently in development
        </h3>
        <p>Release date: when it's ready</p>
        <button class='hoverme' onClick={triggerConfetti}> 
  <span>
    Click for confetti.
  </span>

</button>
      </section>
    </div>
  );
}

export default App;