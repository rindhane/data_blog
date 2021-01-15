
import style from './items.module.css';

let Project= (props)=> {
    const project=props.project;
    return (
        <div className={style.block}>
            <h3>{project.title}</h3>
            <div><button>{project.link}</button></div>
            <ul>
                {project.points.map(point=><li>{point}</li>)}
            </ul> 
            <hr />
        </div>
    );
}

export default Project;
