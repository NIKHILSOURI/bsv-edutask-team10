import React, {useState, useEffect} from 'react'

function App() {

  const [data, setData] = useState([{
    _id: 0,
    description: 'default',
    done: false,
    title: 'test'
  }])

  useEffect(() => {
    fetch('http://localhost:5000/tasks').then(
      res => res.json()
    ).then(
      data => {
        console.log(data)
        setData(data);
        //setData(data.map(d => d.description))
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
          {data.map((task, i) => <li key={task._id}>{task.description}</li>)}
        </ul>
      }
    </div>
  )
}

export default App