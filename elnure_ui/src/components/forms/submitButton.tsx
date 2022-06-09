import './submitButton.css';

export interface SubmitButtonProps {
    label: string;
    className?: string;
    onClick: () => any;
}

const submitButton = (props: SubmitButtonProps) => {
    props.className = props.className && "btn btn-success"
    return (
        <button type="submit" className={props.className}>{props.label}</button>
    )
}

export default submitButton;