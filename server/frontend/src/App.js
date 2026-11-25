import React, {useEffect,useState} from 'react';
import {Routes,Route,useParams,useNavigate} from 'react-router-dom';
import LoginPanel from './components/Login/Login';
import Register from './components/Register/Register';
import Header from './components/Header/Header';

async function api(path, options) {
 const res=await fetch('/djangoapp/'+path,options);
 const data=await res.json();
 if(!res.ok) throw new Error(data.error||data.status||'Request failed');
 return data;
}
function Dealers(){
 const [state,setState]=useState('All'),[dealers,setDealers]=useState([]),[states,setStates]=useState([]),[error,setError]=useState('');
 const user=sessionStorage.getItem('username');
 useEffect(()=>{api('get_dealers').then(d=>setStates([...new Set(d.dealers.map(x=>x.state))].sort())).catch(e=>setError(e.message));},[]);
 useEffect(()=>{setError('');api('get_dealers'+(state==='All'?'':'/'+encodeURIComponent(state))).then(d=>setDealers(d.dealers)).catch(e=>setError(e.message));},[state]);
 return <><Header/><main className="container mt-4"><h1>Dealerships</h1>{!user&&<p><a href="/login">Login</a> | <a href="/register">Register</a></p>}<label htmlFor="state">Filter by State </label><select id="state" value={state} onChange={e=>setState(e.target.value)}><option>All</option>{states.map(s=><option key={s}>{s}</option>)}</select><p role="alert">{error}</p><table className="table table-striped"><thead><tr><th>Dealer</th><th>City</th><th>State</th><th>Address</th>{user&&<th>Review Dealer</th>}</tr></thead><tbody>{dealers.map(d=><tr key={d.id}><td><a href={'/dealer/'+d.id}>{d.full_name}</a></td><td>{d.city}</td><td>{d.state}</td><td>{d.address}</td>{user&&<td><a href={'/postreview/'+d.id}>Post Review</a></td>}</tr>)}</tbody></table></main></>;
}
function Dealer(){
 const {id}=useParams(),[dealer,setDealer]=useState(null),[reviews,setReviews]=useState([]),[error,setError]=useState('');
 useEffect(()=>{Promise.all([api('dealer/'+id),api('reviews/dealer/'+id)]).then(([d,r])=>{setDealer(Array.isArray(d.dealer)?d.dealer[0]:d.dealer);setReviews(r.reviews);}).catch(e=>setError(e.message));},[id]);
 return <><Header/><main className="container mt-4"><p role="alert">{error}</p>{dealer&&<><h1>{dealer.full_name}</h1><p>{dealer.address}, {dealer.city}, {dealer.state}</p></>}{sessionStorage.getItem('username')&&<a href={'/postreview/'+id}>Post Review</a>}<h2>Reviews</h2>{reviews.map(r=><article className="card p-3" key={r.id}><h3>{r.name}</h3><p>{r.review}</p><p>{r.car_make} {r.car_model} {r.car_year}</p><p>Sentiment: {r.sentiment}</p></article>)}</main></>;
}
function Review(){
 const {id}=useParams(),navigate=useNavigate(),[cars,setCars]=useState([]),[error,setError]=useState('');
 const [form,setForm]=useState({review:'',purchase:false,purchase_date:'',car_make:'',car_model:'',car_year:2023});
 useEffect(()=>{api('get_cars').then(d=>setCars(d.CarModels)).catch(e=>setError(e.message));},[]);
 const submit=async e=>{e.preventDefault();try{await api('add_review',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({...form,dealership:Number(id),purchase_date:form.purchase_date||'Not applicable'})});navigate('/dealer/'+id);}catch(e){setError(e.message);}};
 return <><Header/><main className="container mt-4"><h1>Post Review</h1><form onSubmit={submit}><label>Review<textarea className="form-control" required value={form.review} onChange={e=>setForm({...form,review:e.target.value})}/></label><div><label><input type="checkbox" checked={form.purchase} onChange={e=>setForm({...form,purchase:e.target.checked})}/> Purchased a car</label></div><label>Purchase date <input type="date" value={form.purchase_date} onChange={e=>setForm({...form,purchase_date:e.target.value})}/></label><div><label>Car model <select required defaultValue="" onChange={e=>{const c=cars[Number(e.target.value)];if(c)setForm({...form,car_make:c.CarMake,car_model:c.CarModel,car_year:c.CarYear});}}><option value="">Select car</option>{cars.map((c,i)=><option key={i} value={i}>{c.CarMake} {c.CarModel} {c.CarYear}</option>)}</select></label></div><button className="btn btn-primary" type="submit">Submit Review</button><p role="alert">{error}</p></form></main></>;
}
export default function App(){return <Routes><Route path="/login" element={<LoginPanel/>}/><Route path="/register" element={<Register/>}/><Route path="/dealers" element={<Dealers/>}/><Route path="/dealer/:id" element={<Dealer/>}/><Route path="/postreview/:id" element={<Review/>}/><Route path="/" element={<Dealers/>}/></Routes>;}
