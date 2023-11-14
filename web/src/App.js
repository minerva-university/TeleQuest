import React from "react";
import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom";
import "./App.css";
import robot from "./robot.svg";
import AboutPage from "./components/AboutPage";

import JSConfetti from "js-confetti";

const jsConfetti = new JSConfetti();

const App = () => {
  const triggerConfetti = () => {
    jsConfetti.addConfetti();
  };

  return (
    <Router>
      <div className="container">
        <nav>
          <Link to="/">Home</Link>
          <Link to="/about">About</Link>
          <Link to="/contact">Contact</Link>
        </nav>

        <Routes>
          <Route
            path="/"
            element={
              <main>
                <header>
                  <section className="main-content">
                    <h1>TeleQuest</h1>
                    <div id="tagline">
                      <h3>A unique answer</h3>
                      <h3>to the same questions.</h3>
                    </div>

                    <h2>
                      <br />
                      <br />
                      Great for large Telegram** groups
                    </h2>

                    <div className="buttons">
                      <button>Get Started</button>
                    </div>

                    <div id="bottom-main">
                      <p>**Exclusively available through Telegram</p>
                      <div className="buttons">
                        <button className="hoverme" onClick={triggerConfetti}>
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
            }
          />

          <Route path="/about" element={<AboutPage />} />

          {/* If you have a contact component, you can integrate it as shown below. */}
          {/* <Route path="/contact" element={<Contact />} /> */}
        </Routes>
      </div>
    </Router>
  );
};

export default App;
