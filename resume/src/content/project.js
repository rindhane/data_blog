import React from "react";
import style from './items.module.css';

let Project= (props)=> {
    const project=props.project;
    return (
        <div className={style.category}>
            <div>
                <div className={style.padMargin}>
                    <i className="fa fa-sticky-note" aria-hidden="true"></i>
                    <span className={style.title}>{project.title}</span>
                </div>
                <div className={style.sideRight}>
                <i className={["fa", "fa-external-link-square",].join(' ')}><a href={project.link} className={style.textTeal}> Code Repository at GitHub</a></i>
                </div>
                <ul>
                    {project.points.map((point, index)=><li key={index}>{point}</li>)}
                </ul> 
                <hr/>
            </div>
        </div>
    );
}

export default Project;
