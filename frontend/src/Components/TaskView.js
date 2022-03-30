import React, {useState, useEffect} from 'react'
import './../Styles/TaskView.css'

function TaskView(props) {
  function TaskItem(props) {
    return (
      <div className='element' key={props.id}>
        { props.children }
      </div>
    );
  }
  
  function TaskCreator(props) {
    let userid = props.userid
  
    const [title, setTitle] = useState("")
    const [url, setUrl] = useState("")
  
    const submitNewTask = (event) => {
      event.preventDefault()
  
      const data = new URLSearchParams();
      data.append('title', title)
      data.append('description', "")
      data.append('userid', userid)
      data.append('url', url)
      data.append('todos', ['Watch video'])
  
      fetch('http://localhost:5000/tasks/create', {
        method: 'post', 
        body: data
      }).then(res => res.json())
        .then(console.log('updating'))
        .then(updateTasks());
    }
  
    return (
      <form onSubmit={submitNewTask}>
        <div className='inputwrapper'>
          <label>Title</label>
          <input type='text' id='title' name='title' onChange={event => setTitle(event.target.value)}></input>
        </div>
        <div className='inputwrapper'>
          <label>YouTube URL</label>
          <input type='text' id='url' name='url' onChange={event => setUrl(event.target.value)}></input>
        </div>
  
        <button disabled={title.length == 0}>Create new Task</button>
      </form>
    )
  }

  const [tasks, setTasks] = useState([])

  useEffect(() => {
    updateTasks();
  }, []); 

  const updateTasks = () => {
    fetch(`http://localhost:5000/tasks/ofuser/${props.userid}`, {
      method: 'get',
      headers: {'Cache-Control': 'no-cache'}
    })
      .then(res => res.json())
      .then(
        res => {
          // convert the tasks into the required format
          const convertedTasks = res.map(item => {
            return {
              id: item._id['$oid'],
              title: item.title,
              description: item.description,
              url: item.video.url
            }
          });
          // store the received tasks in the state
          setTasks(convertedTasks);
          console.log(tasks);
        }
      ).catch(function(error) {
        console.log(error)
      });
  }

  return (
      <div className='container'>
      {
        tasks.map(task => 
          <TaskItem id={task.id}>
            <a href={`https://www.youtube.com/watch?v=${task.url}`} target='_blank' rel="noreferrer">
              <img src={`http://i3.ytimg.com/vi/${task.url}/hqdefault.jpg`} alt=''></img>
              
              <div className="title-overlay">{task.title}</div>
            </a>
          </TaskItem>)
      }

      <TaskItem id='newtask'>
        <TaskCreator userid={props.userid}/>
      </TaskItem>
    </div>
  );
}

export default TaskView