import  { useState } from 'react';
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
        { id: 1, type: 'Found', itemName: 'ID card', description: 'UITS cse department er floor e ekta id card pawa gese.', matchScore: '98%' },
        { id: 2, type: 'Found', itemName: 'id card', description: 'UITS English department theke ekta ID card pawa gese.', matchScore: '85%' },
    
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
          {loading ? <p className={styles.refreshBtn}>Refreshing...</p> : <p className={styles.refreshBtn}>Refresh</p>}
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