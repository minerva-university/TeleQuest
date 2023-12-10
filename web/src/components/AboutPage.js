// AboutPage.js

import React, { useState } from "react";

const AboutPage = () => {
  const [activeIndex, setActiveIndex] = useState(null);

  const faqData = [
    { question: "Question 1", answer: "Answer to question 1." },
    { question: "Question 2", answer: "Answer to question 2." },
    // Add more FAQ items as needed
  ];

  const handleToggleAnswer = (index) => {
    setActiveIndex((prevIndex) => (prevIndex === index ? null : index));
  };

  return (
    <div className="about-container">
      <p className="about-text">
        TeleQuest is a platform that provides a unique answer for common
        questions. Especially designed for large Telegram groups, TeleQuest
        ensures every member gets the response they need.
      </p>
      {/* FAQ Section */}
      <h2>FAQs:</h2>
      {faqData.map((faqItem, index) => (
        <div key={index} className="faq-item">
          <button
            className="faq-question"
            onClick={() => handleToggleAnswer(index)}
          >
            {faqItem.question}
            {activeIndex === index ? " - Hide Answer" : " + Show Answer"}
          </button>
          {activeIndex === index && (
            <p className="faq-answer">{faqItem.answer}</p>
          )}
        </div>
      ))}
    </div>
  );
};

export default AboutPage;
