import React, { useEffect,useRef, useState} from "react";
//import * as tf from "@tensorflow/tfjs";
import Resumable from "./resumable"
import {
    Form,
    Button,
    Table
   } from "react-bootstrap"


let images;
var imgfile,imgs;
let project_hash_code = '9321f92aa387'
let dataset_hash_code = "f2f6a3cbd574"
let job_hash_code = '7354412e0f64'

    function updateImageDisplay(preview,input) {
        while (preview.firstChild) {
            preview.removeChild(preview.firstChild);
        }

        const curFiles = input.files;
        if (curFiles.length === 0) {
            const para = document.createElement('p');
            para.textContent = '尚未上傳圖片';
            preview.appendChild(para);
        } else {
            const list = document.createElement('table');
            list.border = '1'
            preview.appendChild(list);

            for (const file of curFiles) {
                const listItem = document.createElement('td');
                const para = document.createElement('p');
                if (validFileType(file)) {
                    para.textContent = `File: ${file.name}    Size: ${returnFileSize(file.size)}.`;
                    const image = document.createElement('img');
                    image.src = URL.createObjectURL(file);
                    image.style = "height: 250px;"

                    listItem.appendChild(image);
                    listItem.appendChild(para);
                } else {
                    para.textContent = `${file.name}: Not a valid file type. Update your selection.`;
                    listItem.appendChild(para);
                }

                list.appendChild(listItem);
            }
        }
    }

    const fileTypes = [
        "image/apng",
        "image/bmp",
        "image/gif",
        "image/jpeg",
        "image/pjpeg",
        "image/png",
        "image/svg+xml",
        "image/tiff",
        "image/webp",
        "image/x-icon"
    ];
    const clatype = [
        "Barley_kernels",
        "Barley_kernels",
        "Black_beans",
        "Black_beans",
        "Crystal_rock_sugar",
        "Crystal_rock_sugar",
        "Job_s_tears",
        "Job_s_tears",
        "Red_Job_s_tears",
        "Red_Job_s_tears",
        "Red_rock-sugar",
        "Red_rock-sugar",
        "Shelled_mung_bean",
        "Shelled_mung_bean",
        "mung_bean",
        "mung_bean",
        "soybean",
        "soybean"
    ]
        function validFileType(file) {
        return fileTypes.includes(file.type);
    }

    function returnFileSize(number) {
        if (number < 1024) {
            return number + 'bytes';
        } else if (number >= 1024 && number < 1048576) {
            return (number / 1024).toFixed(1) + 'KB';
        } else if (number >= 1048576) {
            return (number / 1048576).toFixed(1) + 'MB';
        }
    }
    
    
    

const Classify = () => {
    const canvasRef = useRef(null);
    const [ imgState, setimgState ] = useState(true);
    const [ imgData,setimgData ] = useState('');
    const [data, setdata] = useState('')
    
    useEffect(()=>{
        fetch("/get_token").then(res=>res.json()).then(
            data=>{
                setdata(data)
            }
        ) .catch(e => {
            console.log(e)
        })}, [])
    
  
   
    const _upImg = () => {
        
    let r = new Resumable(
        {
            target:'http://125.227.129.220:21720/api/upload_images_in_model',
            simultaneousUploads: 1,
            query:{
                'project_hash_code': project_hash_code,
                'dataset_hash_code': dataset_hash_code ,
                'job_hash_code': job_hash_code
            },
            headers: {
                'X-CSRF-TOKEN': data['csrf_refresh_token'],
                'Authorization':`Bearer ${data['refresh_token']}`
            }
        }
    );
        let event=document.getElementById('upimg')
        console.log(event.files)
        r.addFiles(event.files)
        console.log(r.files)
        r.upload()
        console.log(r.isUploading())
        r.on('complete', function(){
                console.log("com")
          })
        fetch("/upload?type=classification",{method:"GET"}).then(res=>res.json()).then(
            data=>{
                console.log(data)
            }
        ) .catch(e => {
            console.log(e)
        })
        
    }

    const upchange=()=>{
        const input = document.querySelector('#upimg');
        const preview = document.querySelector('.preview');
        console.log(input)
            input.style.opacity = 0;
        
            input.addEventListener('change', updateImageDisplay(preview,input));
        
    }
    const startdetect=()=>{
        let image=document.getElementById("upimg")
        let display=document.getElementById("butts") 
        console.log(image.files[0]['name'])
        fetch('/classify?name='+image.files[0]['name']).then(
                res=>res.text())
            .then(data=>{
              console.log(data)
              display.innerHTML+="<p id='result'}>This is "+clatype[data]+"</p>"
            }
        ) .catch(e => {
            console.log(e)
        })
    }
    return ( 
        <div>
            <div className="preview" style={{overflow: 'scroll', height: '350px', width: '1000px'}}>
                <p>尚未上傳圖片</p>
            </div>
            <form id="file">
                <input id='upimg' type='file'  accept='image/*'  onChange={upchange}  multiple/>

            </form>
            
            <Button onClick={_upImg}>upload</Button>
            <div className="d-grid  butts" style={{marginLeft:'200px'}} id="butts">
            <button   type="button"  className="btn btn-outline-dark col-12" onClick={startdetect}>start detection</button>
            </div>
        </div>
    );

}

export default Classify;