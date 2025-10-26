import React, { useState } from 'react';
import styles from './FindMatches.module.css';
import Button from '../../components/Button/Button';

const FindMatches = () => {
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleRefresh = async () => {
    setLoading(true);
    // Simulate API call
    setTimeout(() => {
      const dummyMatches = [
        { id: 1, type: 'Lost', itemName: 'Red Wallet', description: 'Left in cafe', matchScore: '90%' },
        { id: 2, type: 'Found', itemName: 'Keys with a dog tag', description: 'Found near park entrance', matchScore: '85%' },
        { id: 3, type: 'Lost', itemName: 'iPhone 12', description: 'Lost at bus stop', matchScore: '70%' },
      ];
      setMatches(dummyMatches);
      setLoading(false);
    }, 1500);
  };

  return (
    <div className={styles.matchesContainer}>
      <h2 className={styles.title}>Find Your Matches</h2>
      <div className={styles.actions}>
        <Button onClick={handleRefresh} disabled={loading} variant="primary">
          {loading ? 'Refreshing...' : 'Refresh'}
        </Button>
      </div>

      {loading && <p>Loading matches...</p>}

      {!loading && matches.length === 0 && (
        <p className={styles.noMatches}>No matches found yet. Try refreshing!</p>
      )}

      {!loading && matches.length > 0 && (
        <div className={styles.matchesList}>
          {matches.map((match) => (
            <div key={match.id} className={styles.matchCard}>
              <h3 className={styles.matchItemName}>{match.itemName} ({match.type})</h3>
              <p className={styles.matchDescription}>{match.description}</p>
              <p className={styles.matchScore}>Match Score: <strong>{match.matchScore}</strong></p>
              <Button onClick={() => alert(`Viewing details for ${match.itemName}`)} variant="secondary" className={styles.viewDetailsButton}>
                View Details
              </Button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default FindMatches;