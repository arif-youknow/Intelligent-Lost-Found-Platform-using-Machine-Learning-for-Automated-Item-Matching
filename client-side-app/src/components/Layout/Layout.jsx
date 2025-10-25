import { Link, Outlet } from 'react-router-dom';
import styles from './Layout.module.css';

const Layout = () => {
  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <h1 className={styles.title}>Intelligent Lost & Found Platform</h1>
        <h3 className={styles.subtitle}>using Machine Learning for Automated Item Matching</h3>
        <nav className={styles.nav}>
          <Link to="/" className={styles.navLink}>Home</Link>
          <Link to="/profile" className={styles.navLink}>Profile</Link>
          <Link to="/find-matches" className={styles.navLink}>Find Your Matches</Link>
          {/* Add more global nav links if needed */}
        </nav>
      </header>
      <main className={styles.mainContent}>
        <Outlet /> {/* Renders the current route's component */}
      </main>
      {/* <footer className={styles.footer}>...</footer> */}
    </div>
  );
};

export default Layout;