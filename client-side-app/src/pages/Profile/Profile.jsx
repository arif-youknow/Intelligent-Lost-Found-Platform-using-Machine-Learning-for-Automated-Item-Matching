import React from 'react';
import styles from './Profile.module.css';

const Profile = () => {
  // In a real app, this would fetch user data
  const userData = {
    name: "John Doe",
    email: "john.doe@example.com",
    registeredItems: [
      { id: 'L001', name: 'Blue Backpack', status: 'Lost' },
      { id: 'F001', name: 'Silver Watch', status: 'Found' },
    ],
  };

  return (
    <div className={styles.profileContainer}>
      <h2 className={styles.title}>Your Profile</h2>
      <div className={styles.profileDetails}>
        <p><strong>Name:</strong> {userData.name}</p>
        <p><strong>Email:</strong> {userData.email}</p>
        {/* Add more profile details */}
      </div>

      <h3 className={styles.sectionTitle}>Your Registered Items</h3>
      {userData.registeredItems.length === 0 ? (
        <p>No items registered yet.</p>
      ) : (
        <ul className={styles.itemsList}>
          {userData.registeredItems.map(item => (
            <li key={item.id} className={styles.item}>
              <span className={styles.itemName}>{item.name}</span>
              <span className={`${styles.itemStatus} ${item.status === 'Lost' ? styles.lost : styles.found}`}>
                {item.status}
              </span>
              <button className={styles.viewButton}>View</button>
            </li>
          ))}
        </ul>
      )}

      <button className={styles.editProfileButton}>Edit Profile</button>
    </div>
  );
};

export default Profile;