import React, { useState } from 'react';

export default function QuestionPrompt({ onAskQuestion }) {
    const [questionTitle, setQuestionTitle] = useState('');
    const [questionBody, setQuestionBody] = useState('');

    function handleSubmit(event) {
        event.preventDefault();
        onAskQuestion({
            title: questionTitle,
            body: questionBody,
        });
    }

    return (

        <form onSubmit={handleSubmit}>
            <label>
                Question Title
                <input
                    type='text'
                    placeholder='Ask your question...'
                    value={questionTitle}
                    onChange={e => setQuestionTitle(e.target.value)}
                    className='prompt-title'
                />
            </label>
            <label>
                Question Body
                <input
                    type='text'
                    placeholder='Describe your question...'
                    value={questionBody}
                    onChange={e => setQuestionBody(e.target.value)}
                    className='prompt-title'
                />
            </label>
            <button type='submit' className='prompt-submit' >
                {/* <img src='search-icon.png' className='prompt-submit-icon'
                    onClick={handleSubmit}
                /> */}
                Ask Question
            </button>
        </form>
    );
}
