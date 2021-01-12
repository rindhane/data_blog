import React from "react";

let Project= (props)=> {
    const project=props.project;
    return (
        <div>
            <h3>{project.title}</h3>
            <div><button>{project.link}</button></div>
            <ul>
                {project.points.map(point=><li>{point}</li>)}
            </ul>   
        </div>
    );
}

export default Project;
