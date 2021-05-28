
const mode_DEV=false;

const static_url = (content , isPROD=!mode_DEV) => {
    
    let PREFIX = "";
    let URL="";
    const storage_folder='resume'
    if (isPROD){ PREFIX='/static'}
    if (content==="projects"){URL=`/${storage_folder}/data/projects.json`}
    if (content==="workex"){URL=`/${storage_folder}/data/experience.json`}
    if (content==="introPic"){URL=`/${storage_folder}/data/photo.jpg`}
    if (content==="certificates"){URL=`/${storage_folder}/data/certifications.json`}

    return PREFIX+URL; 

}

export const external_url = (content )=>{
    let link='';
    if (content==="resume"){link="https://drive.google.com/file/d/1Oo-2DhAy8sx-PJYsF2CUA7cmHfoeNafO/view?usp=sharing"}
    if (content==="chat"){link="https://ipassport.info"}
    return link;

}

export default static_url;
