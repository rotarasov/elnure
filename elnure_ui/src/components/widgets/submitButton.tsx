export interface SubmitButtonProps {
    label: string;
    className?: string;
    onClick?: () => any;
}

const submitButton = (props: SubmitButtonProps) => {
    const className = props.className ?? "btn btn-success"
    return (
        <button type="submit" className={className}>{props.label}</button>
    )
}

export default submitButton;