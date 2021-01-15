import React from 'react';
import style from './items.module.css';

let Workex = (props) => {
    let exp=props.exp 
    return (
        <div className={style.block}>
            <h3>{exp.title}</h3>
            <div>{exp.time}</div>
            <ol>
                {exp.points.map(point=>{return (<li>{point}</li>);})}
            </ol>
            <hr/>
        </div>
    )
}

export default Workex;