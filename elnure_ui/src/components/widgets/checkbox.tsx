import './checkbox.css';

export interface DataAttribute {
    name: string;
    value?: any;
}

export interface CheckboxProps {
    label: string;
    value: string;
    id?: string;
    href?: string;
    dataAttrs?: DataAttribute[]
    onChange: (e: React.ChangeEvent<HTMLInputElement>) => void
}

const CheckboxInput = (props: CheckboxProps) => {
    const onChange = props.onChange ?? undefined

    const dataAttrs: Record<string, any> = {}
    props.dataAttrs?.forEach((dataAttr) => {
        dataAttrs[dataAttr.name] = dataAttr.value
    })
    return (
        <div className="form-check mt-3">
            <input {...dataAttrs} className="form-check-input" type="checkbox" id={props.id} value={props.value} onChange={props.onChange} />
            <label className="form-check-label" htmlFor={props.id}>
                {props.label} {props.href && <a href={props.href}><img src="../../../link.png" alt="Link"></img></a>}
            </label>
        </div>
    )
}

export default CheckboxInput;