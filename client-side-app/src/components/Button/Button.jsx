import styles from './Button.module.css';

const Button = ({ children, onClick, variant = 'primary', type = 'button', ...props }) => {
  return (
    <button
      className={`${styles.button} ${styles[variant]}`}
      onClick={onClick}
      type={type}
      {...props}
    >
      {children}
    </button>
  );
};

export default Button;