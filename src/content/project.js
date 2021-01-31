
import style from './items.module.css';

let Project= (props)=> {
    const project=props.project;
    return (
        <div className={style.block}>
            <div>
                <i className="fa fa-sticky-note" aria-hidden="true"></i>
                <span className={style.title}>{project.title}</span>
            </div>
            <div className={style.sideRight}>
                <button>{project.link}</button>
            </div>
            <ul>
                {project.points.map((point, index)=><li key={index}>{point}</li>)}
            </ul> 
            <hr />
        </div>
    );
}

export default Project;
