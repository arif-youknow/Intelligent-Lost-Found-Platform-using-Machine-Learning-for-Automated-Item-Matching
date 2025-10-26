import styles from './InputField.module.css';

const InputField = ({ label, id, type = 'text', value, onChange, placeholder, ...props }) => {
  return (
    <div className={styles.inputGroup}>
      {label && <label htmlFor={id} className={styles.label}>{label}</label>}
      {type === 'textarea' ? (
        <textarea
          id={id}
          className={styles.textarea}
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          {...props}
        />
      ) : (
        <input
          id={id}
          type={type}
          className={styles.input}
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          {...props}
        />
      )}
    </div>
  );
};

export default InputField;