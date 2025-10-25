import { BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import Layout from '../components/Layout/Layout';
import Home from '../pages/Home/Home';
          


const AppRouter = () => { 
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout/>}>
          <Route index element={<Home/>} />
          {/*<Route path="lost-item" element={<LostItemForm />} />
          <Route path="found-item" element={<FoundItemForm />} />
          <Route path="find-matches" element={<FindMatches />} />
          <Route path="profile" element={<Profile />} />
          <Route path="*" element={<div>404 Not Found</div>} />*/}
        </Route>
      </Routes>
    </Router>
  );
};

export default AppRouter; 