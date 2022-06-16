export interface TextInputProps {
    label: string;
    name: string;
    type: string;
    value?: string;
    id?: string;
    href?: string;
    description?: string;
    onChange?: (e: React.ChangeEvent<HTMLInputElement>) => void
}

const TextInput = (props: TextInputProps) => {
    return (
        <div className="form-group">
            <label htmlFor={props.id}>{props.label}</label>
            <input className="form-control" name={props.name} type={props.type} id={props.id} value={props.value} onChange={props.onChange} />
            {props.description && <small id={`${props.id}Help`} className="form-text text-muted">{props.description}</small>}
        </div>
    )
}

export default TextInput;