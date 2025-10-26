import { BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import Layout from '../components/Layout/Layout';
import Home from '../pages/Home/Home';
import FindMatches from '../pages/FindMatches/FindMatches';
import Profile from '../pages/Profile/Profile';
          


const AppRouter = () => { 
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout/>}>
          <Route index element={<Home/>} />
          <Route path="find-matches" element={<FindMatches />} />
          <Route path="profile" element={<Profile />} />
        </Route>
      </Routes>
    </Router>
  );
};

export default AppRouter;