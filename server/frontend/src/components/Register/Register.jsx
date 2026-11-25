import React, { useState } from 'react';
import Header from '../Header/Header';
export default function Register() {
 const [form,setForm]=useState({userName:'',firstName:'',lastName:'',email:'',password:''});
 const [message,setMessage]=useState('');
 const submit=async(e)=>{e.preventDefault();try{const res=await fetch('/djangoapp/register',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(form)});const data=await res.json();if(res.ok && (data.status==='Authenticated'||data.status==='Success')){window.location.href='/login';}else{setMessage(data.message||data.error||'Registration unsuccessful');}}catch{setMessage('Unable to register. Please try again.');}};
 return <><Header/><main style={{maxWidth:480,margin:'40px auto'}}><h1>Sign-up</h1><form onSubmit={submit}>{[['userName','Username','text'],['firstName','First Name','text'],['lastName','Last Name','text'],['email','Email','email'],['password','Password','password']].map(([key,label,type])=><div key={key}><label htmlFor={key}>{label}</label><input id={key} name={key} type={type} required value={form[key]} onChange={e=>setForm({...form,[key]:e.target.value})}/></div>)}<button type="submit">Register</button><p role="status">{message}</p></form></main></>;
}
