import { Link, useNavigate } from 'react-router-dom';
import styles from './Home.module.css';
import Button from '../../components/Button/Button';


const Home = () => {
  const navigate = useNavigate();

  return (
    <div className={styles.homeContainer}>
      <div className={styles.card}>
        <h2 className={styles.cardTitle}>Report an Item</h2>
        <div className={styles.buttonGroup}>
          <Button onClick={() => navigate('/lost-item')} variant="primary">
            Apply for Lost Item
          </Button>
          <Button onClick={() => navigate('/found-item')} variant="secondary">
            Apply for Found Item
          </Button>
        </div>
      </div>

      <div className={styles.infoSection}>
        <h3>Quick Actions</h3>
        <ul>
          <li><Link to="/find-matches" className={styles.infoLink}>Check existing matches</Link></li>
          <li><Link to="/profile" className={styles.infoLink}>View your profile</Link></li>
        </ul>
      </div>
    </div>
  );
};

export default Home;