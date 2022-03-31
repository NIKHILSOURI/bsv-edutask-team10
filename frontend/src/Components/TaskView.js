import React, {useState, useEffect} from 'react'
import './../Styles/TaskView.css'
import './../Styles/Form.css'

function TaskView(props) {
  function TaskItem(props) {
    return (
      <div className='container-element' key={props.id}>
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
        .then(tasklist => convertTasks(tasklist))
        .catch(function(error) {
          console.error(error)
        });
    }
  
    return (
      <form className="submit-form" onSubmit={submitNewTask}>
        <div className='inputwrapper'>
          <label>Title</label>
          <input type='text' id='title' name='title' onChange={event => setTitle(event.target.value)}></input>
        </div>
        <div className='inputwrapper'>
          <label>YouTube URL</label>
          <input type='text' id='url' name='url' onChange={event => setUrl(event.target.value)}></input>
        </div>
  
        <input type="submit" value="Create new Task" disabled={title.length === 0}></input>
      </form>
    )
  }

  const [tasks, setTasks] = useState([])

  useEffect(() => {
    updateTasks();
  }, []); 

  const updateTasks = () => {
    fetch(`http://localhost:5000/tasks/ofuser/${props.user._id}`, {
      method: 'get',
      headers: {'Cache-Control': 'no-cache'}
    })
      .then(res => res.json())
      .then(tasklist => convertTasks(tasklist))
      .catch(function(error) {
        console.error(error)
      });
  }

  const convertTasks = (taskilst) => {
    const convertedTasks = taskilst.map(item => {
      return {
        id: item._id['$oid'],
        title: item.title,
        description: item.description,
        url: item.video.url
      }
    });
    setTasks(convertedTasks);
  }

  return (
      <div className='container'>
      {
        tasks.map(task => 
          <TaskItem id={task.id}>
            <a href={`https://www.youtube.com/watch?v=${task.url}`} target='_blank' rel="noreferrer">
              <img src={`http://i3.ytimg.com/vi/${task.url}/hqdefault.jpg`} alt='' />
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