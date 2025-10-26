import { Link, Outlet } from 'react-router-dom';
import styles from './Layout.module.css';

const Layout = () => {
  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <h1 className={styles.title}>Intelligent Lost & Found Platform</h1>
        <h2 className={styles.subtitle}>using Machine Learning for Automated Item Matching</h2>
        <nav className={styles.nav}>
          <Link to="/" className={styles.navLink}>Home</Link>
          <Link to="/find-matches" className={styles.navLink}>Find Your Matches</Link>
          <Link to="/profile" className={styles.navLink}>Profile</Link>     
        </nav>
      </header>
      <main className={styles.mainContent}>

        <Outlet /> 
        
      </main>
      {/* <footer className={styles.footer}>...</footer> */}
    </div>
  );
};

export default Layout;