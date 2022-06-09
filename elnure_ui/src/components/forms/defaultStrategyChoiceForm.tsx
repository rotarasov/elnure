import { useGet, useUser } from "src/api/hooks";
import Block from "src/data/block";
import Choice from "src/data/choice";
import ElectiveCourse from "src/data/electiveCourse";
import Student from "src/data/student";
import Semester from "src/data/semester";
import CheckboxInput from "./widgets/checkbox";
import { useState } from "react";
import DefaultStrategyValue from "src/data/strategies/default";

export interface ChoiceFormProps {
    user: Student
}

const renderBlock = (block: Block, onClickCheckbox: () => void) => {
    return (
        <div className="card">
            <div className="card-body">
                <div className="card-header">{block.name}</div>
                {block.description && <p className="card-text">{block.description}</p>}
                <hr/>
                <>
                {block.electiveCourses?.map((electiveCourse: ElectiveCourse) => {
                    electiveCourse.name && electiveCourse.id && electiveCourse.shortcut &&
                        <CheckboxInput 
                        label={electiveCourse.name} 
                        name={electiveCourse.shortcut} 
                        value={electiveCourse.id.toString()}
                        id={electiveCourse.id.toString()}
                        href={electiveCourse.syllabus}
                        onClick={onClickCheckbox}
                        />
                })}
                </>
            </div>
        </div>
    )
}

const renderSemester = (semester: Semester, onClickCheckbox: () => void) => {
    return (
        <div className="card">
            <div className="card-header">
                Semester {semester.id}
            </div>
            <div className="card-body d-flex flex-row flex-md-column flex-wrap">
                <>
                {semester.blocks?.map((block: Block) => {
                    renderBlock(block, onClickCheckbox)
                })}
                </>
            </div>
        </div>
    )
}

const DefaultStragetyChoiceForm = (props: ChoiceFormProps) => {
    const [loading, semesters, errors] = useGet<Semester[]>("semesters", {for_user: props.user.id})
    
    const [value, setValue] = useState<DefaultStrategyValue>({})

    const onClickCheckbox = () => {
    }

    return (
        <form>
            <>
            {semesters?.map((semester: Semester) => {
                <div className="row">
                    {renderSemester(semester, onClickCheckbox)}
                </div>
            })}
            </>
            <div className="card">
                <div className="card-header">
                    Actions
                </div>
                <div className="card-body">
                    
                </div>
            </div>
        </form>
    )
}

export default DefaultStragetyChoiceForm;