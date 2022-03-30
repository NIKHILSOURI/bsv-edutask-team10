import React, {useState, useEffect} from 'react'
import './App.css'
import TaskView from './Components/TaskView'
import NavBar from './Components/NavBar'

function App() {
  // create a react state for the list of tasks to display
  const [tasks, setTasks] = useState([])
  const [email, setEmail] = useState('')

  const [user, setUser] = useState({
    "_id": "624442cfa6ba7231cec8f2c2"
  })
  
  useEffect(() => {
    fetch(`http://localhost:5000/tasks/ofuser/${user['_id']}`)
      .then(res => res.json())
      .then(
        tasks => {
          // convert the tasks into the required format
          const convertedTasks = tasks.map(item => {
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
      });
  }, [user]);

  const login = (event) => {
    event.preventDefault();
    console.log(email)
    fetch(`http://localhost:5000/users/bymail/${email}`)
      .then(res => res.json())
      .then(u => {
        u['_id'] = u['_id']['$oid']
        setUser(u)
      })
      .catch(function(error) {
        console.error(error)
      });
  }
  
  return (
    <div>
      <NavBar />

      {(user == null) ?
        <div>
          <form onSubmit={login}>
            <div className='inputwrapper'>
              <label>Email </label>
              <input type='text' id='title' name='title' onChange={event => setEmail(event.target.value)}></input>
            </div>

            <button>Login</button>
          </form>
        </div>
        : <div>
          <h1>Tasks</h1>
          <TaskView
            tasks={tasks}
          />
        </div>}
    </div>
  );
}

export default App