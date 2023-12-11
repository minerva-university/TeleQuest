import React, { useState, useRef, useEffect } from "react";
import "./App.css";
import robot from "./robot.svg";

const App = () => {
  const homeRef = useRef(null);
  const aboutRef = useRef(null);
  const contactRef = useRef(null);

  const [activeButton, setActiveButton] = useState(null);
  const [openQuestions, setOpenQuestions] = useState([]);

  const handleButtonClick = (buttonName) => {
    setActiveButton(buttonName);
  };

  const scrollToHome = () => {
    if (homeRef.current) {
      homeRef.current.scrollIntoView({ behavior: "smooth" });
    }
    handleButtonClick("home");
  };

  const scrollToAbout = () => {
    if (aboutRef.current) {
      aboutRef.current.scrollIntoView({ behavior: "smooth" });
    }
    handleButtonClick("about");
  };

  const scrollToContact = () => {
    if (contactRef.current) {
      contactRef.current.scrollIntoView({ behavior: "smooth" });
    }
    handleButtonClick("contact");
  };

  const toggleQuestion = (question) => {
    setOpenQuestions((prevQuestions) => {
      if (prevQuestions.includes(question)) {
        // If the question is already open, close it
        return prevQuestions.filter((q) => q !== question);
      } else {
        // If the question is closed, open it
        return [...prevQuestions, question];
      }
    });
  };

  const faqData = [
    { question: "Question 1", answer: "Answer to question 1." },
    { question: "Question 2", answer: "Answer to question 2." },
    // Add more FAQ items as needed
  ];

  useEffect(() => {
    // Scroll to homeRef when the component mounts
    scrollToHome(); // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);
  return (
    <div className="container">
      <div className="home-container" ref={homeRef}>
        <nav className="buttons-container">
          <button
            className={`buttons${activeButton === "home" ? " active" : ""}`}
            onClick={scrollToHome}
          >
            Home
          </button>
          <button
            className={`buttons${activeButton === "about" ? " active" : ""}`}
            onClick={scrollToAbout}
          >
            About
          </button>
          <button
            className={`buttons${activeButton === "contact" ? " active" : ""}`}
            onClick={scrollToContact}
          >
            Contact
          </button>
        </nav>

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
                <button className="filled" onClick={scrollToAbout}>
                  Get Started
                </button>
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
      </div>

      {/* AboutPage Section */}
      <div className="about-container" ref={aboutRef}>
        <p className="about-text">
          TeleQuest is a platform that provides a unique answer for common
          questions. Especially designed for large Telegram groups, TeleQuest
          ensures every member gets the response they need. TeleQuest is a
          platform that provides a unique answer for common questions.
          Especially designed for large Telegram groups, TeleQuest ensures every
          member gets the response they need. TeleQuest is a platform that
          provides a unique answer for common questions. Especially designed for
          large Telegram groups, TeleQuest ensures every member gets the
          response they need.
        </p>
        <p className="question"> How does it work? </p>
        <p className="about-text2">
          TeleQuest is a platform that provides a unique answer for common
          questions. Especially designed for large Telegram groups, TeleQuest
          ensures every member gets the response they need. TeleQuest is a
          platform that provides a unique answer for common questions.
          Especially designed for large Telegram groups, TeleQuest ensures every
          member gets the response they need. TeleQuest is a platform that
          provides a unique answer for common questions. Especially designed for
          large Telegram groups, TeleQuest ensures every member gets the
          response they need.
        </p>

        <p className="question"> How does it work? </p>
        <p className="about-text2">
          TeleQuest is a platform that provides a unique answer for common
          questions. Especially designed for large Telegram groups, TeleQuest
          ensures every member gets the response they need. TeleQuest is a
          platform that provides a unique answer for common questions.
          Especially designed for large Telegram groups, TeleQuest ensures every
          member gets the response they need. TeleQuest is a platform that
          provides a unique answer for common questions. Especially designed for
          large Telegram groups, TeleQuest ensures every member gets the
          response they need.
        </p>
        <p className="question"> How does it work? </p>
        <p className="about-text2">
          TeleQuest is a platform that provides a unique answer for common
          questions. Especially designed for large Telegram groups, TeleQuest
          ensures every member gets the response they need. TeleQuest is a
          platform that provides a unique answer for common questions.
          Especially designed for large Telegram groups, TeleQuest ensures every
          member gets the response they need. TeleQuest is a platform that
          provides a unique answer for common questions. Especially designed for
          large Telegram groups, TeleQuest ensures every member gets the
          response they need.
        </p>

        {/* FAQ Section */}
        <h2 className="faq-title">FAQs:</h2>
        <div className="faq-container">
          {faqData.map((faqItem, index) => (
            <div key={index} className="faq-item">
              <button
                className="faq-question"
                onClick={() => toggleQuestion(faqItem.question)}
              >
                {faqItem.question}
              </button>
              {openQuestions.includes(faqItem.question) && (
                <p className="faq-answer">{faqItem.answer}</p>
              )}
            </div>
          ))}
        </div>
      </div>
      <div className="contact-container" ref={contactRef}>
        <p className="greatPitch">Contact</p>
        <p className="about-text">
          TeleQuest is a platform that provides a unique answer for common
          questions. Especially designed for large Telegram groups, TeleQuest
          ensures every member gets the response they need.
        </p>
        <p className="about-text2">
          TeleQuest is a platform that provides a unique answer for common
          questions. Especially designed for large Telegram groups, TeleQuest
          ensures every member gets the response they need.
        </p>
        <p className="about-text">
          TeleQuest is a platform that provides a unique answer for common
          questions. Especially designed for large Telegram.
        </p>
      </div>
    </div>
  );
};

export default App;
