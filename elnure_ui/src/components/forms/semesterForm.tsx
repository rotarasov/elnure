import { useApplicationWindow, useGet, useUser } from "../../api/hooks";
import Block from "../../data/block";
import ElectiveCourse from "../../data/electiveCourse";
import Student from "../../data/student";
import CheckboxInput from "../widgets/checkbox";
import SubmitButton from "../widgets/submitButton";
import React, { useState, useEffect } from "react";
import DefaultStrategyChoiceValue from "../../data/strategies/default";
import { useParams, Link, Navigate } from "react-router-dom";
import { ApiError, post } from "../../api";
import ApplicationWindow from "../../data/applicationWindow";
import { Strategy } from "../../data/strategies";

const renderBlock = (block: Block, onClickCheckbox: (e: React.ChangeEvent<HTMLInputElement>) => void) => {
    return (
        <div className="card mt-3 card-primary card-outline">
            <div className="card-body">
                <div className="card-title"><b>{block.name}</b></div>
                {block.description && <p className="card-text">{block.description}</p>}
                <hr/>
                <>
                {block.electiveCourses?.map((electiveCourse: ElectiveCourse) => {
                    return electiveCourse.name && electiveCourse.id && electiveCourse.shortcut &&
                        <CheckboxInput 
                        label={electiveCourse.name} 
                        value={electiveCourse.id.toString()}
                        id={`elective-course-${electiveCourse.id}`}
                        href={electiveCourse.syllabus}
                        onChange={onClickCheckbox}
                        dataAttrs={[{name: "data-block-id", value: block.id?.toString()}, {name: "data-elective-course-id", value: electiveCourse.id.toString()}]}
                        />
                })}
                </>
            </div>
        </div>
    )
}

const SemesterForm = () => {
    const params = useParams();
    const [loading, blocks, errors] = useGet<Block[]>("ref/blocks", {semester: params.semesterId})
    const [choiceValue, setChoiceValue] = useState<DefaultStrategyChoiceValue[]>([])
    const [user, setUser] = useState<Student>();
    const [applicationWindow, setApplicationWindow] = useState<ApplicationWindow>();
    const [success, setSuccess] = useState<boolean>(false);

    useEffect(() => {
        async function fetchUser() {
            return await useUser();
        }

        fetchUser().then(data => setUser(data)).catch((e) => console.log(`User fetch error: ${e}`))

        async function fetchApplicationWindow() {
            return await useApplicationWindow();
        }

        fetchApplicationWindow().then(data => setApplicationWindow(data)).catch((e) => console.log(`Application window fetch error: ${e}`))
    }, [])

    const onChangeCheckbox = (e: React.ChangeEvent<HTMLInputElement>) => {
        const electiveCourseId = parseInt(e.target.dataset.electiveCourseId || "0");
        const blockId = parseInt(e.target.dataset.blockId || "0");
        
        if (electiveCourseId == 0 || blockId == 0) {
            throw new Error("Incorrectly set data ids.");
        }

        const isChecked = e.target.checked;

        const newChoiceValue: DefaultStrategyChoiceValue[] = []
        if (isChecked) {
            let updated = false;
            choiceValue.forEach((choice) => {
                if (choice.blockId == blockId) {
                    choice.electiveCourseIds?.push(electiveCourseId)
                    updated = true;
                }
                newChoiceValue.push(choice)
            })
            if (!updated) {
                newChoiceValue.push({blockId, electiveCourseIds: [electiveCourseId]})
            }
        } else {
            choiceValue.forEach((choice) => {
                if (choice.blockId == blockId) {
                    const newElectiveCourseIds: number[] = []
                    choice.electiveCourseIds?.forEach((selectElectiveCourseId) => {
                        if (selectElectiveCourseId != electiveCourseId) {
                            newElectiveCourseIds.push(electiveCourseId)
                        }                        
                    })
                    choice.electiveCourseIds = newElectiveCourseIds
                }
                newChoiceValue.push(choice)
            });
        }
        setChoiceValue(newChoiceValue);
        
    }

    const onSubmit = async (e: React.SyntheticEvent<HTMLElement>) => {
        e.preventDefault()

        if (!user || !user.id || !applicationWindow || !applicationWindow.id) {
            throw new Error("Not all items are set.")
        }

        const choice = {
            student: user.id,
            application_window: applicationWindow.id,
            semester: params.semesterId,
            value: choiceValue,
            strategy: Strategy.DEFAULT
        }

        try {
            await post<DefaultStrategyChoiceValue>("choices", choice)
            setSuccess(true);
        } catch(e) {
            console.log(`Choice post error: ${JSON.stringify((e as ApiError).body)}`)
        }
    }

    if (success) {
        return <Navigate to="/success"/>
    }

    return (
        <form onSubmit={onSubmit}>
            <>
            {blocks?.map((block: Block) => {
                return renderBlock(block, onChangeCheckbox)
            })}
            </>
            <div className="card mt-3">
                <div className="card-body">
                    <SubmitButton label="Save" className="btn btn-block btn-success"/>
                </div>
                <div className="card-footer text-muted d-flex justify-content-center">
                    <Link to="/application-window" className="text-center">Back to application window</Link>
                </div>
            </div>
        </form>
    )
}

export default SemesterForm;