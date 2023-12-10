import React from "react";
import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom";
import "./App.css";
import robot from "./robot.svg";
import AboutPage from "./components/AboutPage";
import { NavLink } from "react-router-dom";

const App = () => {
  return (
    <Router>
      <div className="container">
        <nav className="buttons-container">
          <NavLink to="/" className="buttons" activeClassName="active">
            Home
          </NavLink>
          <NavLink to="/about" className="buttons" activeClassName="active">
            About
          </NavLink>
          <NavLink to="/contact" className="buttons" activeClassName="active">
            Contact
          </NavLink>
        </nav>

        <Routes>
          <Route
            path="/"
            element={
              <main>
                <header>
                  <section className="main-content">
                    <h1 className="title">TeleQuest</h1>
                    <div className="tagline">
                      <h3 className="pitchLeft">A unique answer</h3>
                      <h3 className="pitchRight">to the same questions.</h3>
                    </div>

                    <h2 className="greatPitch">
                      <br />
                      <br />
                      Great for large Telegram** groups
                    </h2>
                    <h4 className="button-start">
                      <button>Get Started</button>
                    </h4>
                    <h5 className="exclusiveMessage">
                      **Exclusively available through Telegram
                    </h5>
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
