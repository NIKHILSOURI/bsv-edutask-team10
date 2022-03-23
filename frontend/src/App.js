import React, {useState, useEffect} from 'react'
import './App.scss'

function App() {
  // create a react state for the list of tasks to display
  const [tasks, setTasks] = useState([])
  

  useEffect(() => {
    fetch('http://localhost:5000/tasks/John/Doe').then(
      // cast the received data to json
      res => res.json()
    ).then(
      user => {
        // convert the tasks into the required format
        console.log(user)

        const convertedTasks = user['tasks'].map(item => {
          return {
            id: item._id['$oid'],
            title: item.title,
            description: item.description,
            url: item.video.url
          }
        });
        // store the received tasks in the state
        setTasks(convertedTasks);
      }
    ).catch(function(error) {
      console.log(error)
    })
  }, [])

  return (
    <div>
      <h1>Tasks</h1>
      <div className='container'>
        {
          tasks.map(task => 
            <div className='element'>
              <a href={`https://www.youtube.com/watch?v=${task.url}`} target='_blank'>
                <img src={`http://i3.ytimg.com/vi/${task.url}/hqdefault.jpg`}></img>
              </a>
              <div className="title-overlay">{task.title}</div>
            </div>)
        }
      </div>
    </div>
  );
}

export default App