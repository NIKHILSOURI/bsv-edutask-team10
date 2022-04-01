import React, {useState} from 'react'
import './../Styles/TaskDetail.css'

import Editable from './Editable';

function TaskDetail( { task, updateTasks } ) {
    const [todo, setTodo] = useState("");

    const addTodo = (e) => {
        e.preventDefault();

        if(todo === "") {
            return;
        }
        
        const data = new URLSearchParams();
        data.append('taskid', task._id);
        data.append('description', todo);
        
        fetch('http://localhost:5000/todos/create', {
            method: 'post',
            body: data,
            headers: {'Cache-Control': 'no-cache'}
        })
            .then(res => res.json())
            .then(todoobj => {
                // update the tasks in the background
                updateTasks();

                // add the new todo element to the list
                task.todos.push({
                    _id: todoobj['_id']['$oid'],
                    description: todoobj['description'],
                    done: todoobj['done']
                });

                // reset todo
                setTodo("");
            })
            .catch(function(error) {
                console.error(error)
            });
    }

    return (
        <div>
            <h1>
                <Editable objectname="tasks" object={task} variablename="title" updateTasks={updateTasks} />
            </h1>

            <p>
                <Editable objectname="tasks" object={task} variablename="description" updateTasks={updateTasks} />
            </p>

            <a href={`https://www.youtube.com/watch?v=${task.url}`} target='_blank' rel="noreferrer">
                <img src={`http://i3.ytimg.com/vi/${task.url}/hqdefault.jpg`} alt='' />
                </a>
            <ul className='todo-list'>
                {task.todos.map(todo => 
                    <li key={todo._id} className='todo-item'>
                        <Editable objectname="todos" object={todo} variablename="description" updateTasks={updateTasks} />
                    </li>)
                }
                <li key='newtodo'>
                    <form onSubmit={addTodo} className='inline-form'>                    
                        <input type='text' onChange={e => setTodo(e.target.value)} value={todo}placeholder='Add a new todo item'></input>
                        <input type='submit' value='Add'></input>
                    </form>
                </li>
            </ul>
        </div>
    );
}

export default TaskDetail