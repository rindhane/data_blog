
const mode_DEV=false;

const static_url = (content , isPROD=!mode_DEV) => {
    
    let PREFIX = "";
    let URL="";
    if (isPROD){ PREFIX='/static'}
    if (content==="projects"){URL='/about/data/projects.json'}
    if (content==="workex"){URL='/about/data/experience.json'}
    if (content==="introPic"){URL='/about/data/photo.jpg'}
    if (content==="certificates"){URL='/about/data/certifications.json'}

    return PREFIX+URL; 

}

export const external_url = (content )=>{
    let link='';
    if (content==="resume"){link="https://drive.google.com/file/d/1Oo-2DhAy8sx-PJYsF2CUA7cmHfoeNafO/view?usp=sharing"}
    if (content==="chat"){link="https://ipassport.info"}
    return link;

}

export default static_url;
