import {Link} from "react-router-dom"

export interface SuccessPageProps {
    semesterId: number|string
}

const SuccessPage = (props: SuccessPageProps) => {
    return (
        <div>
            <h3>{`Thank you for choosing elective subjects for Semester ${props.semesterId}`}</h3>
            <p className="text-center"><Link to="/application-window">Choose for another semester</Link></p>
        </div>
    )
}

export default SuccessPage;