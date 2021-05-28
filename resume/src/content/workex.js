import React from 'react';
import style from './items.module.css';

let Workex = (props) => {
    let exp=props.exp 
    return (
        <div className={style.category}>
            <div className={style.padMargin}>
                <div>
                    <h3>{exp.title}</h3>
                </div>
                <div className={style.sideRight}>
                <i className="fa fa-calendar"> {exp.time}</i>
                <span></span>
                <i className="fa fa-building-o " aria-hidden="true"></i>
                <span>{exp.organization}</span>
                </div>
                <ol>
                    {exp.points.map((point,index)=>{return (<li key={index}>{point}</li>);})}
                </ol>
                <hr/>
            </div>
        </div>
    )
}

export default Workex;