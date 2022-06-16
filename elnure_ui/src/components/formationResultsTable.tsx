import { useEffect, useState } from "react"
import { useParams } from "react-router"
import { ApiError } from "src/api";
import { FormationResult } from "src/data/formationResult";
import { getFormationResults } from "../api/core"
import { Link } from "react-router-dom"

const renderElectiveCourse = (electiveCourseData: Record<string, any>) => {
    return (
        <div className="card">
            {Object.keys(electiveCourseData).map((electiveGroupName: string) => {
                return (
                    <div className="card-body">
                        <div className="card-title">{electiveGroupName}</div>
                        <div className="table table-stripped">
                        <tbody>
                            {electiveCourseData[electiveGroupName].map((student: string[]) => {
                                // Skipping email to leave more spaces
                                return (
                                    <tr>
                                        <th scope="row">{student[0]}</th>
                                        <td>{student[2]}</td>
                                        <td>{student[3]}</td>
                                    </tr>
                                )    
                            })}
                        </tbody>
                        </div>
                    </div>
                )
            })}
        </div>
    )
}


const renderSemester = (semesterData: Record<string, any>) => {
    return (
        <div className="card">
            <div className="card-header">
                {semesterData.name}
            </div>
            <div className="card-body">
            {Object.keys(semesterData.data).map((electiveCourseName: string) => {
                return (
                    <div className="card">
                        <div className="card-body">
                            <div className="card-title">{electiveCourseName}</div>
                            {renderElectiveCourse(semesterData.data[electiveCourseName])}
                        </div>
                    </div>
                )
            })}
            </div>
        </div>
    )
}


const FormationResultsTable = () => {
    const params = useParams();
    const [formationResults, setFormationResults] = useState<FormationResult[]>([])

    useEffect(() => {
        const fetchData = async () => {
            return await getFormationResults(params.appWindowId as string)
        }

        fetchData().then((result) => setFormationResults(result)).catch((e) => console.log(JSON.stringify((e as ApiError).body)))
    })

    return (
        <div>
            <div className="row ml-2 mb-3">
                <Link to="/application-window">Go back</Link>
            </div>
            <div className="row">
                {formationResults.map((formationResult: Record<string, any>) => {
                    return (
                        <div className="col">
                            {renderSemester(formationResult)}
                        </div>
                    )
                })}
            </div>
        </div>
    )
}

export default FormationResultsTable