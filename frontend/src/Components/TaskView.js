import React, {useState, useEffect} from 'react'
import './../Styles/TaskView.css'
import './../Styles/Form.css'
import Popup from './../Components/Popup'
import TaskDetail from './TaskDetail'

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
  const [focus, setFocus] = useState({})
  const [trigger, setTrigger] = useState(false)

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

  const convertTasks = (tasklist) => {
    let convertedTasks = []
    for(const task of tasklist) {
      let todolist = []
      for(const todo of task.todos) {
        todolist.push({
          _id: todo['_id']['$oid'],
          description: todo.description,
          done: todo.done
        })
      }

      convertedTasks.push({
        _id: task['_id']['$oid'],
        title: task.title,
        description: task.description,
        url: task.video.url,
        todos: todolist
      });
    }
    setTasks(convertedTasks);
  }

  /*return (
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
      <Popup trigger={trigger} setTrigger={setTrigger}>
          <h3>Hi</h3>
        </Popup>
      <TaskItem id='newtask'>
        <TaskCreator userid={props.userid}/>
      </TaskItem>
    </div>
  );*/
  return (
    <div className='container'>
    {
      tasks.map(task => 
        <TaskItem id={task.id}>
          <a onClick={() => {setTrigger(true); setFocus(task)}}>
            <img src={`http://i3.ytimg.com/vi/${task.url}/hqdefault.jpg`} alt='' />
            <div className="title-overlay">{task.title}</div>
          </a>
        </TaskItem>)
    }

    <TaskItem id='newtask'>
      <TaskCreator userid={props.userid}/>
    </TaskItem>

    
    {trigger && 
      <Popup trigger={trigger} setTrigger={setTrigger}>
        <TaskDetail taskid={focus._id} updateTasks={updateTasks}/>
      </Popup>
    }
  </div>
);
}

export default TaskView