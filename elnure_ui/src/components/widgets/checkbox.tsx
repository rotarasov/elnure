export interface CheckboxProps {
    label: string;
    value: string;
    name: string;
    id?: string;
    href?: string;
    onClick: () => void
}

const CheckboxInput = (props: CheckboxProps) => {
    props.onClick = props.onClick ?? undefined
    return (
        <div className="form-check">
            <input className="form-check-input" type="radio" name={props.name} id={props.id} value={props.value} onClick={props.onClick} />
            <label className="form-check-label" htmlFor={props.id}>
                { props.href ? <a href={props.href}>{props.label}</a> : <>{props.label}</> }
            </label>
        </div>
    )
}

export default CheckboxInput;