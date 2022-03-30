import React from 'react'
import './../Styles/TaskView.css'

const TaskView = props => {
    const submitNewTask = (event) => {
        console.log(event)
    }

    return (
        <div className='container'>
        {
          props.tasks.map(task => 
            <div className='element' key={task.id}>
              <a href={`https://www.youtube.com/watch?v=${task.url}`} target='_blank' rel="noreferrer">
                <img src={`http://i3.ytimg.com/vi/${task.url}/hqdefault.jpg`} alt=''></img>
              </a>
              <div className="title-overlay">{task.title}</div>
            </div>)
        }

        <div className='element' key='newtask'>
          <button>Create new Task</button>
          <form onSubmit={submitNewTask}>
            <div className='inputwrapper'>
              <label>Title </label>
              <input type='text' id='title' name='title'></input>
            </div>
            <div className='inputwrapper'>
              <label>Description </label>
              <input type='text' id='description' name='description'></input>
            </div>

            <button>Save</button>
          </form>
        </div>
      </div>
    );
}

export default TaskView