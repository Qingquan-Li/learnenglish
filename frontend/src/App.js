import React, { Component } from 'react';
import axios from 'axios'; // new

class App extends Component {
  // state = {
  //   todos: []
  // };
  constructor(props) {
    // In JavaScript classes, you need to always call super when defining the constructor of a subclass.
    // All React component classes that have a constructor should start with a super(props) call.
    super(props);
    this.state = {
      sentences: []
    };
  }

  // new
  componentDidMount() {
    this.getSentences();
  }

  // new
  getSentences() {
    axios
      .get('http://localhost:8000/api/v1/words-in-sentences/sentences/')
      .then(res => {
        this.setState({ sentences: res.data.results });
      })
      .catch(err => {
        console.log(err);
      });
  }

  render() {
    return (
      <div>
        {this.state.sentences.map(item => (
          <div key={item.id}>
            <h4>{item.english_sentence}</h4>
            <span style={{color: "green"}}>{item.highlight_word}</span>
          </div>
        ))}
      </div>
    );
  }
}

export default App;
