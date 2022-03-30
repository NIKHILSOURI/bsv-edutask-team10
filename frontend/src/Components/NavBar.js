import React, { useState} from 'react';
import './../Styles/NavBar.css'

// import icons
import { ReactComponent as CaretIcon } from './../Icons/caret.svg';
import { ReactComponent as ArrowIcon } from './../Icons/arrow.svg';

function NavBar(props) {
    return (
        <nav className="navbar">
            <ul className="navbar-nav">
                <NavItem icon="😴" />
                <NavItem icon={<CaretIcon />}>
                    <DropdownMenu />
                </NavItem>
            </ul>
        </nav>
    );
}

function NavItem(props) {
    const [open, setOpen] = useState(false);

    return (
        <li className='nav-item'>
            <a href='#' className='icon-button' onClick={() => setOpen(!open)}>
                {props.icon}
            </a>

            
            {open && props.children}
        </li>
    );
}

function DropdownMenu() {
    function DropdownItem(props) {
        return (
            <a href='#' className="menu-item">
                <span className='icon-button'>{props.leftIcon}</span>
                {props.children}
            </a>
        )
    }

    return (
        <div className='dropdown'>
            <DropdownItem>My Tasks</DropdownItem>
            <DropdownItem>My Profile</DropdownItem>
            <DropdownItem leftIcon={<ArrowIcon />}>Logout</DropdownItem>
        </div>
    );
}

export default NavBar