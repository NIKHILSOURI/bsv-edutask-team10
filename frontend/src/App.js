import React, {useState, useEffect} from 'react'
import './App.scss'

function App() {
  // create a react state for the list of tasks to display
  const [data, setData] = useState([{
    id: 0,
    title: 'Learn react',
    description: 'Learn the fundamentals of the react JS frontend framework',
    done: false
  }])

  return (
    <div>
      <h1>Tasks</h1>
      <div className='container'>
        <div className='element'>
          <a href='https://www.youtube.com/watch?v=QdHvS0D1zAI' target='_blank'>
            <img src='http://i3.ytimg.com/vi/QdHvS0D1zAI/hqdefault.jpg'></img>
          </a>
          <div className="title-overlay">Hosting a Website on Raspberry Pi</div>
        </div>
        <div className='element'>
          <a href='https://www.youtube.com/watch?v=Sxxw3qtb3_g' target='_blank'>
            <img src='http://i3.ytimg.com/vi/Sxxw3qtb3_g/hqdefault.jpg'></img>
          </a>
          <div className="title-overlay">Tech Stacks</div>
        </div>
        <div className='element'>
          <a href='https://www.youtube.com/watch?v=Qhaz36TZG5Y' target='_blank'>
            <img src='http://i3.ytimg.com/vi/Qhaz36TZG5Y/hqdefault.jpg'></img>
          </a>
          <div className="title-overlay">CSS Tips</div>
        </div>
      </div>
    </div>
  );

  /*useEffect(() => {
    fetch('http://localhost:5000/tasks').then(
      // cast the received data to json
      res => res.json()
    ).then(
      data => {
        // convert the tasks into the required format
        const convertedTasks = data.map(item => {
          return {
            id: item._id['$oid'],
            title: item.title,
            description: item.description,
            done: item.done
          }
        });
        // store the received tasks in the state
        setData(convertedTasks);
      }
    ).catch(function(error) {
      console.log(error)
    })
  }, [])

  return (
    <div>
      {data.length === 0 ? 
        <p>not there</p> : 
        <ul>
          {data.map((task, i) => <li key={task.id}>{task.title}: {task.description} {task.done ? 'done' : 'not done'}</li>)}
        </ul>
      }
    </div>
  )*/
}

export default App