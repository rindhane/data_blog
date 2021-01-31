import style from './items.module.css';

let Education = (props) => {
    let course = {
        title:'Bachelor of Technology in Mechanical Engineering',
        time:'2020-Present',
        points: ['Compliant Mechanism @ IISc',
                 'Baja Vehicle Development',
                  'Wind simulation for India’s wind potential']
    }; 
    return (
        <div className={style.block}>
            <h3>{course.title}</h3>
            <div className={style.sideRight}>
                <span>2007-2011 </span>
                <i className="fa fa-university" aria-hidden="true"></i>
                <span>IIT BHU, Varanasi</span>
            </div>
            <div>Projects\Thesis Submitted:</div>
            <ul>
            {course.points.map((point,index)=>{return (<li key={index}>{point}</li>);})}
            </ul>
            <hr/>
        </div>
    )
}

export default Education;