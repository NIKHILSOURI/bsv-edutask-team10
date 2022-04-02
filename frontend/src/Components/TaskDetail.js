import React, { useState, useEffect } from 'react'
import './../Styles/TaskDetail.css'

import Editable from './Editable';

function TaskDetail({ taskid, updateTasks }) {
    const [task, setTask] = useState(null);
    const [todos, setTodos] = useState([]);
    const [todo, setTodo] = useState("");

    useEffect(() => {
        updateTask();
    }, []);

    const updateTask = () => {
        fetch(`http://localhost:5000/tasks/byid/${taskid}`, {
            method: 'get',
            headers: { 'Cache-Control': 'no-cache' }
        })
            .then(res => res.json())
            .then(tobj => {
                let todolist = []
                for (const todobj of tobj.todos) {
                    todolist.push({
                        _id: todobj['_id']['$oid'],
                        description: todobj.description,
                        done: todobj.done
                    })
                }
                setTodos(todolist);
                setTask({
                    _id: tobj['_id']['$oid'],
                    title: tobj.title,
                    description: tobj.description,
                    url: tobj.video.url
                });
            })
    }

    const addTodo = (e) => {
        e.preventDefault();

        if (todo === "") {
            return;
        }

        const data = new URLSearchParams();
        data.append('taskid', task._id);
        data.append('description', todo);

        fetch('http://localhost:5000/todos/create', {
            method: 'post',
            body: data,
            headers: { 'Cache-Control': 'no-cache' }
        })
            .then(res => res.json())
            .then(todoobj => {
                updateTask();

                // reset todo
                setTodo("");
            })
            .catch(function (error) {
                console.error(error)
            });
    }

    const toggleTodo = (todo) => {
        const data = new URLSearchParams();
        data.append('data', `{'$set': {'done': ${!todo.done}}}`);

        fetch(`http://localhost:5000/todos/byid/${todo._id}`, {
            method: 'put',
            body: data,
            headers: { 'Cache-Control': 'no-cache' }
        })
            .then(res => res.json())
            .then(updateTask())
            //.then(updateTasks())
    }

    const deleteTodo = (todo) => {
        fetch(`http://localhost:5000/todos/byid/${todo._id}`, {
            method: 'delete',
            headers: { 'Cache-Control': 'no-cache' }
        })
            .then(res => res.json())
            .then(res => console.log(res))
            .then(updateTask())
    }

    return (
        task == null ? 
        <p>Loading</p> :
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
                {todos.map(todo =>
                    <li key={todo._id} className='todo-item'>
                        <span className={'checker ' + (todo.done ? 'checked' : 'unchecked')} onClick={() => toggleTodo(todo)}></span>
                        <Editable objectname="todos" object={todo} variablename="description" updateTasks={updateTasks} />
                        <span className='remover' onClick={() => deleteTodo(todo)}>&#x2716;</span>
                    </li>)
                }
                <li key='newtodo'>
                    <form onSubmit={addTodo} className='inline-form'>
                        <input type='text' onChange={e => setTodo(e.target.value)} value={todo} placeholder='Add a new todo item'></input>
                        <input type='submit' value='Add'></input>
                    </form>
                </li>
            </ul>
        </div>
    );
}

export default TaskDetail