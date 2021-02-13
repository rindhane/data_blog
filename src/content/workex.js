import React from 'react';
import style from './items.module.css';

let Workex = (props) => {
    let exp=props.exp 
    return (
        <div className={style.category}>
            <h3>{exp.title}</h3>
            <div className={style.sideRight}>{exp.time}</div>
            <ol>
                {exp.points.map((point,index)=>{return (<li key={index}>{point}</li>);})}
            </ol>
            <hr/>
        </div>
    )
}

export default Workex;