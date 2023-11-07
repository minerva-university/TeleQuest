import React from "react";
import "./App.css";
import robot from "./robot.svg";

import JSConfetti from "js-confetti";

const jsConfetti = new JSConfetti();

const App = () => {
  const triggerConfetti = () => {
    jsConfetti.addConfetti();
  };
  return (
    <div className="container">
      {/* I think need to move this one to a navbar up top? */}

      <nav>
        <button>Home</button>
        <button>About</button>
        <button>Contact</button>
      </nav>

      <main>
        <header>
          <section className="main-content">
            <h1>TeleQuest</h1>
            <div id="tagline">
              <h3>A unique answer</h3>
              <h3>to the same questions.</h3>
            </div>

            <h2><br/><br/>Great for large Telegram** groups</h2>

            <div className="buttons">
              <button>Get Started</button>
            </div>

            <div id="bottom-main">
              <p>**Exclusively available through Telegram</p>
              <div className="buttons">
                <button class="hoverme" onClick={triggerConfetti}>
                  <span>Click for confetti.</span>
                </button>
              </div>
            </div>
          </section>
        </header>

        <div className="illustration">
          <img src={robot} alt="Chatbot Illustration" />
        </div>
      </main>
    </div>
  );
};

export default App;
